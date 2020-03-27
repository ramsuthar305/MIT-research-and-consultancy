import React, { useState } from 'react'
import 'bootstrap/dist/css/bootstrap.min.css';
import { Form, Button } from 'react-bootstrap';
import axios from 'axios'


function RegisterForm() {
    return (
        <div>
            <Form className="w-50 m-auto" >
                <Form.Group controlId="formBasicEmail">
                    <Form.Label>Email address</Form.Label>
                    <Form.Control type="email" o placeholder="Enter email" />
                </Form.Group>
                <Form.Group controlId="formBasicEmail">
                    <Form.Label>Name</Form.Label>
                    <Form.Control type="text" o placeholder="name" />
                </Form.Group>
                <Form.Group controlId="formBasicEmail">
                    <Form.Label>Phone</Form.Label>
                    <Form.Control type="text" o placeholder="Enter email" />
                </Form.Group>

                <Form.Group controlId="formBasicPassword">
                    <Form.Label>Password</Form.Label>
                    <Form.Control type="password" placeholder="Password" />
                </Form.Group>
                <Button variant="primary" type="submit">
                    Submit
                </Button>
            </Form>
        </div>
    )
}

export default RegisterForm