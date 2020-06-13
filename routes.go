package main

import (
	//"net/http"

	"encoding/json"
	"github.com/dandelabs/ghostbuster-backend-registration/api"
	"github.com/dandelabs/ghostbuster-backend-registration/cclog"
	"github.com/dandelabs/ghostbuster-backend-registration/response"
	"github.com/dandelabs/ghostbuster-backend-registration/router"
	"github.com/gorilla/mux"
	"io"
	"net/http"
)

// Constant regex and params
const (
	token         = "{token}"
	link          = "{link}"
	regexUUID     = "[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}"
	regexEmaiil   = "{email:\\w[-._\\w]*\\w@\\w[-._\\w]*\\w\\.\\w{2,3}}"
	UUID          = "{uuid:" + regexUUID + "}"
	dependentUUID = "{uuid_dependent:" + regexUUID + "}"
	permission    = "{permission}"
)

//All routes should be added here
const (
	// VERSION = "v2"
	// we need home for ELB to stay alive
	HOME = "/"
	// /api/user
	postCreateUser = "/api/user"
)

var routes = router.Routes{

	/****HOME****/
	router.Route{
		Name:        "HOME",
		Method:      "GET",
		Pattern:     HOME,
		NeedToken:   false,
		HandlerFunc: router.Home,
	},
	/****CREATE NEW USER****/
	router.Route{
		"Create new user",
		"POST",
		postCreateUser,
		false,
		func(w http.ResponseWriter, r *http.Request) {
			PostManager(w, r, api.CreateUser)
		},
	},
}

// PostManager handles all HTTP POST requests
func PostManager(w http.ResponseWriter, r *http.Request,
	fToRun func(map[string]string, io.ReadCloser) *response.Response) {
	method := "PostManager:"

	var statusCode int
	var errorCode int
	var res *response.Response
	if r.Method != "POST" {
		http.Error(w, http.StatusText(405), 405)
		return
	}

	params := GetBasicParams(r)
	res = fToRun(params, r.Body)
	js, err1 := json.Marshal(res)
	w.Header().Set("Content-Type", "application/json")
	if err1 != nil {
		w.WriteHeader(500)
		res := response.BuildResponse(response.CONST_ERROR, response.E500_INTERNAL_SERVER_ERROR, "Internal server error: "+err1.Error())
		//res := &response.Response{Type:response.CONST_ERROR,Content:"Internal server error: "+err1.Error()}
		js, _ := json.Marshal(res)
		w.Write(js)

		return
	}
	if res.Type == response.CONST_ERROR || res.Type == response.CONST_ERROR_INTERNAL {
		errorCode = res.Content.(map[string]interface{})["code"].(int)
		statusCode = getResponseStatusCode(errorCode)
		w.WriteHeader(statusCode)
	} else if res.Type == response.CONST_ERROR_USER {
		errorCode = res.Content.(map[string]interface{})["code"].(int)
		statusCode = getResponseStatusCode(errorCode)
		w.WriteHeader(statusCode)
	} else if res.Type == response.CONST_PASSWORD_RESET {
		w.Write([]byte("Password reset successfully!"))
		return
	}

	cclog.Info.Println(method, "response:", string(js))
	w.Write(js)
}

func GetBasicParams(r *http.Request) map[string]string {
	method := "getBasicParams:"
	params := mux.Vars(r)
	cclog.Trace.Println(method + "header")
	cclog.Trace.Println(r.Header)

	/*params["device_token"] = getHeaderDeviceToken(r)
	params["push_token"] = getHeaderDevicePushToken(r)
	cclog.Info.Println("PushToken:", params["push_token"], "|")
	params["device_type"] = getHeaderDeviceType(r)
	params["device_id"] = getHeaderDeviceID(r)
	params["ids_scope"] = r.Form.Get("ids_scope")
	params["client_id"] = getHeaderClientID(r)
	params["client_secret"] = getHeaderClientSecret(r)
	params["password"] = getHeaderPassword(r)
	params["scope"] = r.Header.Get("scope")
	params["user_id"] = r.Header.Get("user_id")
	params["client_ip"] = r.RemoteAddr*/
	//q := r.FormValue("q")
	//params["q"] = q

	return params
}

func getResponseStatusCode(code int) int {
	switch code {
	case 1, 2, 3, 4, 5, 6, 7, 16, 21:
		return 401
	case 8, 9, 10, 15, 17, 20:
		return 404
	case 11, 12, 18, 19:
		return 409
	case 13:
		return 500
	case 14:
		return 498
	}
	return 200
}
