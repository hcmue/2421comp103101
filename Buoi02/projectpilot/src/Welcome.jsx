import { useState } from "react"

export const Hello = () => {
    const [name, setName] = useState("Tèo");
    return (
        <>
            <input value={name} onChange={ (v) => {
                console.log(v)
                setName(v)
            }} />
            <div>Xin chào {name}</div>
        </>
    )
}