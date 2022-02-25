import { response } from 'express';
import { async } from 'q';
import React, { useState } from 'react';
import '../../../App.css';


export const CreateAdmin = () => {

    const [username, setUsername] = useState<string>("");
    const [password, setPassword] = useState<string>("");

    const handleCreateAdmin = async (e: any) => {
        e.preventDefault();

        // TODO: add usernamer and password validations
        
        fetch('/test/add_admin',
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
                alert("Admin created successfully")
            } 
            else {
                alert("A problem occured")
            }
        })
    }

    return(
        <div id="login-form">
            <form onSubmit={(handleCreateAdmin)}>
                
                <div className='container'>
                    <label htmlFor="Username"><b>New Username </b></label>
                    <input id="Username"
                        type="text"
                        placeholder="Enter Username"
                        onChange={({ target }) => {setUsername(target.value)}}
                    />

                    <label htmlFor="Password"><b>New Password </b></label>
                    <input id="Password"
                        type="password"
                        placeholder="Enter your password"
                        onChange={({ target }) => {setPassword(target.value)}}
                    />
                </div>

                <div id="button">
                    <button type="submit">Create</button>
                </div>
            </form>
        </div>
    )    
}