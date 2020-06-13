package db

import (
	"database/sql"
	"errors"
	"github.com/dandelabs/ghostbuster-backend-registration/cclog"
	"github.com/dandelabs/ghostbuster-backend-registration/crypt"
)

const (
	StateUserActive   = "ACTIVE"
	StateUserInactive = "INACTIVE"
)

// User struct stores all user information
type User struct {
	ID        string
	FirstName string `sql:"first_name" json:"First_name"`
	LastName  string `sql:"last_name" json:"Last_name"`
	NickName  string `sql:"nick_name" json:"Nick_name"`
	Password  string
}

func InsertUser(user User) (id string, err error) {
	method := "insertUser:"
	cclog.Trace.Println(method)
	var userID string
	var result sql.Result

	hash, salt, err := crypt.GenerateEncryptPassword(user.Password)
	if err != nil {
		return userID, err
	}

	result, err = dbCon.Exec("INSERT INTO pfoptimization.users(first_name, "+
		" last_name, nick_name, password, salt, created, updated, state) "+
		" VALUES(?,?,?,?,?, (UNIX_TIMESTAMP(now())), "+
		"(UNIX_TIMESTAMP(now())), ?)",
		user.FirstName, hash, salt, StateUserActive)

	if err == nil {
		nRows, err := result.RowsAffected()
		cclog.Info.Println(method+"number of user created%d", nRows)
		if nRows == 0 || err != nil {
			err = errors.New("New users were not inserted")
			return userID, err
		}
	}
	return "0", err
}
