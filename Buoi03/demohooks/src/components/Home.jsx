import { useContext } from "react";
import { MyContext } from "../MyContext";
export const Home = () => {
    const {username, isLogged } = useContext(MyContext);
    console.log(username, isLogged)
    return (
        <>
            <h2>HOME PAGE</h2>
            {isLogged && (
                <div>WELCOME MY PRO</div>
            )}
            {isLogged ? (
                <div>Chào mừng bạn <strong>{username}</strong> thăm trang của tui</div>
            ) : (
                <div>Bạn chưa đăng nhập</div>
            )}
        </>
    )
};