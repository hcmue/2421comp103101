import { createContext } from "react";

//định nghĩa thông tin cần lưu trữ và chia sẽ trong Context
export const MyContext = createContext({
    isLogged: false,
    username: '',
    setIsLogged: () => {},
    setUsername: () => {}
});

export const MyContextProvider = ({ children }) => {
    const [username, setUsername] = useState(null);
    const [isLogged, setIsLogged] = useState(false);
    return (
        <MyContext.Provider value={{
            username,
            setUsername,
            isLogged,
            setIsLogged
        }}>
            {children}
        </MyContext.Provider>
    )
}