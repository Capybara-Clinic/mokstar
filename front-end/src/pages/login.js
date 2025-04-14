import { useState, useContext, useEffect } from "react";
import { useNavigate  } from "react-router-dom";
import FirebaseContext from "../context/firebase";

// near 1:20:00 part, read that

export default function Login() {
    const navigate = useNavigate ();
    const {firebase} = useContext(FirebaseContext);

    const [emailAddress, setEmailAddress] = useState('');
    const [password, setPassword] = useState('');

    const [error, setError] = useState('');
    const isInvalid = password === '' || emailAddress === '';

    const handleLogin = () => {};

    useEffect(() => {
        document.title = 'Login - Mokstagram';
    }, []) 

    return ( // tailwind?
        <div className="container flex mx-auto max-w-screen-md items-center h-screen">
            <div className="flex w-3/5">
                <img src="images/capybara-pace-to-face.jpg" alt="the capybara"></img>
            </div>
        </div>
    );
}