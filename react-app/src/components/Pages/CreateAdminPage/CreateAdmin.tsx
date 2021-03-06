import { response } from 'express';
import { async } from 'q';
import React, { useEffect, useState } from 'react';
import { server_url } from '../../../app-constants';
import '../../../App.css';


export const CreateAdmin = () => {

    const [username, setUsername] = useState<string>("");
    const [password, setPassword] = useState<string>("");
    const [confirmPassword, setConfirmPassword] = useState<string>("");
    const [admins, setAdmins] = useState<string[]>([]);

    const handleCreateAdmin = async (e: any) => {
        e.preventDefault();
        console.log("Username: " + username + " Pass: " + password);

        if(username.length < 3) {
            alert("Username should be at least 3 characters");
        }
        else if(!username.match("^[A-Za-z0-9]+$")) {
            alert("Username can contain only letters and numbers");
        }
        else if(!username.charAt(0).match("^[A-Za-z]+$")) {
            alert("The username must start with a letter");
        }
        else if(password.length < 5) {
            alert("Password should be at least 5 characters");
        }
        else if(!password.match("^[A-Za-z0-9!@#$%^&*]+$")) {
            alert("Password can contain only letters, numbers, !, @, #, $, %, ^, & and *");
        }
        else if(password !== confirmPassword) {
            alert("Passwords are not the same");
        }
        else {
            await fetch(`${server_url}/add_admin`,
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
                    alert("Admin created successfully");
                    getAdmins();
                } 
                else if(resp.status === 409) {
                    alert("This admin username is taken. Please select a different name.");
                }
                else {
                    alert("A problem occured");
                }    
            });
        }
    }

    const getAdmins = async () => {
        await fetch(`${server_url}/get_all_admins`)
        .then(data => data.json())
        .then(data => { 
            let adminsList: string[] = [];
            data.admins.forEach((element: any) => {
                    const newAdmin: string = (
                        element as string);
                        adminsList.push(newAdmin);
            });
            setAdmins(adminsList);
        })
        .catch(e => {
            alert("A problem occured with uploading admins list");
        });
    }

    useEffect(() => {
        getAdmins();
    }, []);

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
                    <input id="Confirm Password"
                        type="password"
                        placeholder="Enter your password again"
                        onChange={({ target }) => {setConfirmPassword(target.value)}}
                    />
                </div>

                <div id="button">
                    <button type="submit">Create</button>
                </div>
            </form>
            <h2>Current Admins List</h2>
            <ul style={{textAlign: 'left', marginLeft: '47%'}}>
            {
                admins.length > 0 ?
                admins.map(admin =>
                    <li style={{}}>
                        {admin}
                    </li>)
            :
            <h2> No Admins Created Yet </h2>
            }
            </ul>
        </div>
    )    
}