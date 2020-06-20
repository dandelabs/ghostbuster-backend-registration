//STATUS CODES https://www.ietf.org/rfc/rfc2616.txt
//http://tools.ietf.org/html/rfc4918

package api

import (
	"encoding/json"
	"net/http"

	"encoding/base64"
	"errors"
	"github.com/dandelabs/ghostbuster-backend-registration/cclog"
	"github.com/dandelabs/ghostbuster-backend-registration/db"
	"github.com/dandelabs/ghostbuster-backend-registration/response"
	"io"
	"strings"
)

func GetMachines(params map[string]string) (res *response.Response) {
	method := "GetMachines"
	cclog.Trace.Printf("%s %+v", method, params)
	machines, err := db.GetMachines()
	if err != nil {
		res = response.BuildResponse(response.CONST_ERROR, response.E404_USER_NOT_FOUND, err.Error())
	} else {
		res = &response.Response{Type: response.CONST_MACHINES, Content: machines}
	}
	return res
}

// CreateUser POST /api/user - creates a primary caregiver account
func CreateUser(params map[string]string, body io.ReadCloser) (res *response.Response) {
	//Get data from request and decode into User struct
	method := "CreateUser"
	var u db.UserMachine
	var userID int64
	err := json.NewDecoder(body).Decode(&u)
	if err != nil {
		cclog.Error.Println(method + err.Error())
		res = response.BuildResponse(response.CONST_ERROR,
			response.E409_INVALID_JSON_OBJECT,
			"Error related with body format:"+err.Error())
		return res
	}
	//Insert user into db
	userID, err = db.InsertUser(u)
	if err != nil {
		cclog.Error.Println(method + "1:" + err.Error())
		res = response.BuildResponse(response.CONST_ERROR_USER, response.E500_INTERNAL_SERVER_ERROR, err.Error())

	} else {
		cclog.Info.Println(method + "Success")
		res = &response.Response{Type: response.CONST_UUID, Content: userID}
	}
	return res
}

//ValidateUserPass /api/password/validation
func ValidateUserPass(w http.ResponseWriter, r *http.Request) {

	method := "ValidateUserPass:"
	var err error
	var nickname string
	var password string
	var code int
	var res *response.Response
	var js []byte
	var ok bool

	jr := make(map[string]interface{})

	w.Header().Set("Content-Type", "application/json")
	nickname, password, code, err = getNicknamePassword(r.Header.Get("Authorization"))

	if err != nil {
		w.WriteHeader(401)
		cclog.Error.Println(method + err.Error())
		res = response.BuildResponse(response.CONST_ERROR, code, err.Error())
		js, _ = json.Marshal(res)
		w.Write(js)
		return
	}

	ok, _, err = db.ValidateLogin(nickname, password)
	// If not valid
	if !ok {
		w.WriteHeader(401)
		if err != nil {
			cclog.Error.Println(method + err.Error())
			cclog.Info.Println("here the user does not exist:" + err.Error())
			res = response.BuildResponse(response.CONST_ERROR, response.E401_USER_DOESNT_EXIST, "Username does not exist.")
		} else {
			w.WriteHeader(401)
			res = response.BuildResponse(response.CONST_ERROR, response.E401_WRONG_PASSWORD, "Wrong username or password.")
		}
		cclog.Info.Println(method, res.Type)
		cclog.Info.Println(method, res.Content)
		js, _ = json.Marshal(res)
		w.Write(js)
		return
	}
	jr["role"] = "test"
	res = &response.Response{Type: "login_role", Content: jr}
	w.WriteHeader(200)
	res = response.BuildResponse(response.CONST_SUCCEED, response.SUCCESS_CODE, "login successfully")
	js, _ = json.Marshal(res)
	w.Write(js)

}

func getNicknamePassword(str string) (nickname, password string, code int, err error) {
	method := "getNicknamePassword: "
	s := strings.SplitN(str, " ", 2)
	cclog.Trace.Println(method + str)
	cclog.Trace.Println(method, s)
	if len(s) < 2 {
		err = errors.New("Not enough parameters")
		cclog.Error.Println(method + err.Error())
		code = response.E401_WRONG_AUTH_HEADER
		return "", "", code, err
	}
	if !strings.EqualFold(s[0], "basic") {
		err = errors.New("Wrong authorization header")
		code = response.E401_WRONG_AUTH_HEADER
		return "", "", code, err
	}

	b, err := base64.StdEncoding.DecodeString(s[1])
	pair := strings.SplitN(string(b), ":", 2)
	if len(pair) != 2 {
		err = errors.New("Missing username or pasword")
		code = response.E401_USER_PASS_NOT_IN_HEADER
		return "", "", code, err
	}
	nickname = pair[0]
	password = pair[1]
	return nickname, password, code, err
}
