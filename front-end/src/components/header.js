import { useContext } from "react";
import FirebaseContext from "../context/firebase";
import UserContext from "../context/user";

export default function Header() {
    const { user } = useContext(UserContext);

    console.log('user', user)

    return (
        <p>I am the header</p>
    );
}