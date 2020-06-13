package router

import (
	"net/http"

	"github.com/gorilla/mux"
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
