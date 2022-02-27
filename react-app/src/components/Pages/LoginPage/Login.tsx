import { response } from 'express';
import { async } from 'q';
import React, { useState } from 'react';
import '../../../App.css';
import { server_url } from '../../../app-constants';


export interface LoginProps {
    page: number;
    setPage: React.Dispatch<React.SetStateAction<number>>;
    isLoggedIn: boolean;
    setIsLoggedIn: React.Dispatch<React.SetStateAction<boolean>>;
}

export const Login: React.FC<LoginProps> = ({
    page,
    setPage,
    isLoggedIn,
    setIsLoggedIn
}) => {

    const [username, setUsername] = useState<string>("");
    const [password, setPassword] = useState<string>("");

    const handleLogin = async (e: any) => {
        e.preventDefault();

        if(
            (username.length < 3) ||
            (username.length > 10) ||
            (!username.match("^[A-Za-z0-9]+$")) ||
            (!username.charAt(0).match("^[A-Za-z]+$")) ||
            (password.length < 5) ||
            (password.length > 12) ||
            (!password.match("^[A-Za-z0-9!@#$%^&*]+$"))
            ) {
            alert("username or password are incorrect");
            return;
        }
        
        await fetch(`${server_url}/test/login`,
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
                setPage(0);
            } else if(resp.status === 404) {
                alert("No admin under this username");
            } else if(resp.status === 401) {
                alert("Admin logging-in failed");
            }
            else {
                alert("username or password are incorrect");
            }
        });
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