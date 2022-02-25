import { response } from 'express';
import { async } from 'q';
import React, { useState } from 'react';
import '../../../App.css';


export interface LoginProps {
    isLoggedIn: boolean;
    setIsLoggedIn: React.Dispatch<React.SetStateAction<boolean>>;
}

export const Login: React.FC<LoginProps> = ({
    isLoggedIn,
    setIsLoggedIn
}) => {

    const [username, setUsername] = useState<string>("");
    const [password, setPassword] = useState<string>("");

    const handleLogin = async (e: any) => {
        e.preventDefault();

        // TODO: add usernamer and password validations
        
        fetch('/test/login',
            {
                method: 'GET',
                headers: {
                    'username': username,
                    'password': password,
                    'Content-Type': 'application/json'   
                }
            })
        .then(resp => {
            if(resp.status === 200) {
                setIsLoggedIn(true);
            } 
            else {
                alert("username or password are incorrect")
            }
        })
    }

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
                    <button type="submit">Login</button>
                </div>
            </form>
        </div>
    )    
}