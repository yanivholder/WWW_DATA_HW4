import { async } from 'q';
import React, { useState } from 'react';
import '../../../App.css';


export interface LoginProps {
    isLoggedIn: boolean;
    setIsLoggedIn: React.Dispatch<React.SetStateAction<boolean>>;
    failedLogin: boolean;
    setFailedLogin: React.Dispatch<React.SetStateAction<boolean>>;
}

export const Login: React.FC<LoginProps> = ({
    isLoggedIn,
    setIsLoggedIn,
    failedLogin,
    setFailedLogin
}) => {

    const [username, setUsername] = useState<string>("");
    const [password, setPassword] = useState<string>("");

    const handleLogin = async (e: any) => {
        setFailedLogin(!failedLogin);
    }

    // TODO: add some photo
    // <div className="imgcontainer">
    //     <img src="img_avatar2.png" alt="Avatar" class="avatar">
    // </div>
    return(
        <div id="login-form">
            <form onSubmit={(handleLogin)}>
                
                <div className='container'>
                    <label htmlFor="Username"><b>Username </b></label>
                    <input id="Username"
                        type="text"
                        placeholder="Enter Username"
                        onChange={({ target }) => {setUsername(target.value)}}
                    />

                    <label htmlFor="Password"><b>Password </b></label>
                    <input id="Password"
                        type="password"
                        placeholder="Enter your password"
                        onChange={({ target }) => {setPassword(target.value)}}
                    />
                </div>

                <div id="button">
                    {
                        failedLogin ?
                        <p> Wrong username or password </p>
                        : <p></p>
                    }
                    <button type="submit">Login</button>
                </div>
            </form>
        </div>
    )    
}