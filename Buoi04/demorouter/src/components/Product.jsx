import { useEffect, useState } from "react"

export const Product =() => {
    const [products, setProducts] = useState([]);
    useEffect(() => {
        fetch("https://api.escuelajs.co/api/v1/products")
            .then(response => response.json())
            .then(json => setProducts(json))
    }, []);
    return (
        <div>
            <h2>PRODUCT PAGE</h2>
            <div>Total {products.length} product(s).</div>
            {products.map((item, idx)=> {
                // console.log(item)
                return (
                    <div key={idx} class="grid grid-5 not-content">
                        <article>
                            <img loading="lazy" src={item.images[0]} alt={item.title} style={{width: 100, height: 120}} /> <p>${item.price}</p>
                            <h4>{item.title}</h4> 
                        </article>
                    </div>
                )
            }
            )}
        </div>
    )
}