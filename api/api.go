//STATUS CODES https://www.ietf.org/rfc/rfc2616.txt
//http://tools.ietf.org/html/rfc4918

package api

import (
	"encoding/json"

	"html/template"
	"io"

	"os"

	"github.com/dandelabs/ghostbuster-backend-registration/cclog"
	"github.com/dandelabs/ghostbuster-backend-registration/db"
	"github.com/dandelabs/ghostbuster-backend-registration/response"
)

// ServiceName for config
const ServiceName = "registration"

var secretKey string
var templates *template.Template
var clientID string

func init() {
	method := "init:"
	err := db.StartDBCon("eddie:C4r0l1na!@tcp(localhost:3306)/pfoptimization")
	if err != nil {
		cclog.Error.Println(method + " It could not database connection:" + err.Error())
		os.Exit(3)
	}

}

// CreateUser POST /api/user - creates a primary caregiver account
func CreateUser(params map[string]string, body io.ReadCloser) (res *response.Response) {
	//Get data from request and decode into User struct
	method := "CreateUser"
	var u db.User
	var userID string
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
