import React, { useState } from 'react'
import 'bootstrap/dist/css/bootstrap.min.css';
import { Form, Button } from 'react-bootstrap';
import axios from 'axios'
import { Link } from 'react-router-dom';


function Login() {
    const [email, setEmail] = useState('')
    const [password, setPassword] = useState('')
    const handleEmail = (event) => {
        setEmail(event.target.value)
    }

    const handlePassword = (event) => {
        setPassword(event.target.value)
    }

    const handleSubmit = async (event) => {
        const body = {
            "email": email,
            "password": password
        }
        event.preventDefault()
        await axios.post('http://localhost:5000/api/users/login/', body)
            .then(response => alert(JSON.stringify(response.data)))
            .catch(error => alert(error))
            setEmail('')
            setPassword('')
    }

    return (
        <div>
            <Form className="w-50 m-auto" onSubmit={handleSubmit}>
                <Form.Group controlId="formBasicEmail">
                    <Form.Label>Email address</Form.Label>
                    <Form.Control vlaue={email} type="email" onChange={handleEmail} placeholder="Enter email" />
                    {email}
                </Form.Group>

                <Form.Group controlId="formBasicPassword">
                    <Form.Label>Password</Form.Label>
                    <Form.Control value={password} type="password" onChange={handlePassword} placeholder="Password" />
                    {password}
                </Form.Group>
                <Button variant="primary" type="submit">
                    Submit
                </Button>
                <Link to="/register">Register</Link>
            </Form>
        </div>
    )
}

export default Login