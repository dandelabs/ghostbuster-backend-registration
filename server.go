package main

import (
	"fmt"
	"github.com/dandelabs/ghostbuster-backend-registration/cclog"
	"github.com/dandelabs/ghostbuster-backend-registration/router"
	"net/http"
	"os"
)

const (
	valHTTPS = "https://"
	valHTTP  = "http://"
)

//Log is created to give the format to the logs
func Log(handler http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		cclog.Info.Printf("%s %s %s", r.RemoteAddr, r.Method, r.URL)
		handler.ServeHTTP(w, r)
	})
}

//Run server
func main() {
	fmt.Println("Hello, world.")
	method := "main:"
	var err error
	var mux = router.NewRouter(routes)
	//fs := http.FileServer(http.Dir("./public/"))
	//mux.PathPrefix("/api/web/public/").Handler(http.StripPrefix("/api/web/public/", fs))
	cclog.InitLog(os.Stdout, os.Stdout, os.Stdout, os.Stderr)
	cclog.Info.Printf("%s, Protocol 2: %s", method, "http")
	err = http.ListenAndServe(":8080", Log(mux))

	if err != nil {
		panic(err)
	}
}
