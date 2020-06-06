# web

import jester


const REG_FORM = """
    <form method=post>
        <input type=text name=email>
        <button type=submit>sub</button>
    </form>
"""

settings:
    # host = Ip
    port = Port(12345)

routes:
    get "/":
        resp "<pre>Hello\n\n" #& $hello
    get "/reg":
        resp REG_FORM
    post "/reg":
        redirect "/" & request.params["email"]
    get "/@email":
        resp "email: $1".format(@"email")
