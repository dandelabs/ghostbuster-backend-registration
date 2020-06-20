package api

import (
	"os"
	"github.com/dandelabs/ghostbuster-backend-registration/cclog"
	"github.com/dandelabs/ghostbuster-backend-registration/db"
	"github.com/dandelabs/ghostbuster-backend-registration/config"
)

var cfg *config.Config

func init() {
	method := "init:"
	environment := os.Getenv("environment")
	config.SetEnvironment(environment)
	cfg = &config.Cfg
	err := db.StartDBCon(cfg.DB.URL)
	if err != nil {
		cclog.Error.Println(method + " It could not database connection:" + err.Error())
		os.Exit(3)
	}

}
