import {useState} from "react";
import '../App.css'

function AuthForm() {
    const [count, setCount] = useState(0)

    return (


        <div className="cpBox">
            <div className="logo"><a href="/"><img src="/rsrc/img/speed.png"/></a></div>
            <form className="login jxi"><h1>Sign in</h1>
                <div className="uiIn"><input type="text" name="username" placeholder="&nbsp;" required=""/> <span
                    className="ph">Email or Username</span><span className="hint">Enter a valid Email address or Username.</span>
                </div>
                <div className="bbAr"><input type="submit" className="uiBtn" value="Next"/></div>
                <div className="subOpt"><a href="/checkpoint/recovery">Forgot Username?</a><a
                    href="/checkpoint/signup">Sign Up</a></div>
            </form>
        </div>

    )

}

export default AuthForm