package main

import (
	//"net/http"

	"github.com/dandelabs/ghostbuster-backend-registration/api"
	"github.com/dandelabs/ghostbuster-backend-registration/router"

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
	postCreateUser   = "/api/user"
	postValidateUser = "/api/user/validate"
	getMachines      = "/api/machines"
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

	router.Route{
		Name:      "Get all machines",
		Method:    "GET",
		Pattern:   getMachines,
		NeedToken: false,
		HandlerFunc: func(w http.ResponseWriter, r *http.Request) {
			router.GetManager(w, r, api.GetMachines)
		},
	},

	router.Route{
		"Create new user",
		"POST",
		postCreateUser,
		false,
		func(w http.ResponseWriter, r *http.Request) {
			router.PostManager(w, r, api.CreateUser)
		},
	},

	router.Route{
		"Validate user credentials",
		"POST",
		postValidateUser,
		false,
		api.ValidateUserPass,
	},
}
