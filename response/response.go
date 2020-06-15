package response

type Response struct {
	Type    string
	Content interface{}
}

const (
	CONST_UUID           = "user_id"
	CONST_USER_INFO      = "user_info"
	CONST_DEPENDENT_UUID = "dependent_uuid"
	CONST_USER_STATUS    = "user_status"
	CONST_BLOB_URL       = "blob_url"
	CONST_SUCCEED        = "success"
	CONST_ERROR          = "error"
	CONST_ERROR_USER     = "error_user"
	CONST_ERROR_INTERNAL = "error_internal"
	CONST_TOKEN_EXP      = "token_expired"
	CONST_PASSWORD_RESET = "password_reset"
	CONST_UPDATE_DEVICE  = "device_token_updated"
	CONST_MACHINES       = "machines"
	CONST_SESSIONS       = "sessions"
	CONST_CONT_URL       = "recordings-url"
	CONST_CAREGIVER_URL  = "caregiver-url"
	CONST_SHORTLINK      = "shortlink"
	CONST_MAIL_SENT      = "mail_sent"
	CONST_SESSIONS_INFO  = "sessions_info"
	CONST_HELP_FILES     = "help_files"

	CONST_SESSION_LIST = "session_list"
)

func BuildResponse(resType string, code int, reason string) (res *Response) {
	var output = make(map[string]interface{})
	output["code"] = code
	output["reason"] = reason
	res = &Response{Type: resType, Content: output}
	return res
}

func HandleResponse(res *Response) (resType string, resCode int, resReason string) {
	resType = res.Type
	resCode = res.Content.(map[string]interface{})["code"].(int)
	resReason = res.Content.(map[string]interface{})["reason"].(string)
	return resType, resCode, resReason
}
