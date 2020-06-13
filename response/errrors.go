package response

/*
401 - "unauthorized"
1 - "wrong authorization header" // /api/login
2 - "username/password not present in header" // /api/login
3 - "username does not exist" // /api/login
4 - "wrong password"	// /api/login
5 - "Access token expired"
6 - "Refresh token invalid"
7 - "Unauthorized"
//PUT


// POST
409 - "conflict"
1 - "email already exists" // /api/user //POST /api/user/:uuid/dependent //POST /api/user/:uuid/dependents?type//=:type
2 - "conflict"

500
1 - "Internal server error "+ log(optional)


404 - "not found"
1 - "email not found" // GET /api/user/mail/:email
2 - "user not found"  // GET /api/user/:uuid //GET /api/user/:uuid/status (uuid)
3 - "URL not Generated" //GET /api/user/:uuid/blob-image /api/user/:uuid/blob-image/:ext
//PUT
// /api/user/:email/dependents/:uuid/:type/:state
*/
const (
	SUCCESS_CODE = iota //0
	// 401
	E401_WRONG_AUTH_HEADER       // 1
	E401_USER_PASS_NOT_IN_HEADER // 2
	E401_USER_DOESNT_EXIST       // 3
	E401_WRONG_PASSWORD          // 4
	E401_ACCES_TKN_EXPIRED       // 5
	E401_REFRESH_TKN_INVALID     // 6
	E401_UNAUTHORIZED            // 7
	// 404
	E404_EMAIL_NOT_FOUND // 8
	E404_USER_NOT_FOUND  // 9
	E404_URL_NOT_GEN     // 10
	// 409
	E409_EMAIL_ALREADY_EXIST // 11
	E409_CONFLICT            // 12
	// 500
	E500_INTERNAL_SERVER_ERROR // 13
	// 498
	E498_URL_EXPIRED // 14
	// new codes after this line
	E404_CLIENT_NOT_FOUND    //15
	E401_EMAIL_NO_CONFIRMED  //16
	E404_SHORTLINK_NOT_FOUND //17
	// Invalid email
	E409_INVALID_EMAIL // 18
	//409 Invalid json
	E409_INVALID_JSON_OBJECT // 19
	E404_OBJECT_NOT_FOUND    //20

	// Third party login
	E401_THIRD_PARTY // 21

	// 400 Bad requests
	E400_BAD_REQUEST //22
)
