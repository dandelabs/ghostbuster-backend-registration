package router

import (
	"encoding/json"
	"github.com/dandelabs/ghostbuster-backend-registration/cclog"
	"github.com/dandelabs/ghostbuster-backend-registration/response"
	"github.com/gorilla/mux"
	"io"
	"net/http"
)

// Route type struct contains attribute of mux routes
type Route struct {
	Name        string
	Method      string
	Pattern     string
	NeedToken   bool
	HandlerFunc http.HandlerFunc
}
type Routes []Route

// NewRouter creates a mux.Router handler based on the routes given
func NewRouter(routes Routes) *mux.Router {
	router := mux.NewRouter()
	for _, route := range routes {
		var handler http.Handler
		handler = route.HandlerFunc
		// if !route.NeedToken {
		// 	handler = CheckAPIGatewayHeader(route.HandlerFunc)
		// } else {
		// 	handler = CheckAPIGatewayHeader(oauth2.CheckToken(route.HandlerFunc, authHost, authPort))
		// }
		router.
			Methods(route.Method).
			Path(route.Pattern).
			Name(route.Name).
			Handler(handler)
	}
	return router
}

func Home(w http.ResponseWriter, r *http.Request) {
	w.Write([]byte("Hello!"))
}

func GetManager(w http.ResponseWriter, r *http.Request,
	fToRun func(map[string]string) *response.Response) {
	var res *response.Response
	method := "GetManager:"
	cclog.Trace.Println(method)
	//GET methods only
	r.ParseForm()
	if r.Method != "GET" {
		http.Error(w, http.StatusText(405), 405)
		return
	}
	cclog.Trace.Println(method)

	params := GetBasicParams(r)

	res = fToRun(params)
	w.Header().Set("Content-Type", "application/json")
	js, err1 := json.Marshal(res)
	if err1 != nil {
		w.WriteHeader(500)
		res := response.BuildResponse(response.CONST_ERROR,
			response.E500_INTERNAL_SERVER_ERROR,
			"Internal server error: "+err1.Error())
		js, _ := json.Marshal(res)
		w.Write(js)

		return
	}
	if res.Type == response.CONST_ERROR {
		errorCode := res.Content.(map[string]interface{})["code"].(int)
		statusCode := getResponseStatusCode(errorCode)
		w.WriteHeader(statusCode)
	} else if res.Type == response.CONST_ERROR_INTERNAL {
		errorCode := res.Content.(map[string]interface{})["code"].(int)
		statusCode := getResponseStatusCode(errorCode)
		w.WriteHeader(statusCode)
	}

	cclog.Info.Println(method, "response:", string(js))
	w.Write(js)
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
