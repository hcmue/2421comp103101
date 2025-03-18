import { Routes, Route, Link} from 'react-router-dom'
import { Home } from './components/Home'
import { Product } from './components/Product'
import { Profile, ChangePassword } from './components/Profile'
import { NoMatch } from './components/NoMatch'
function App() {

  return (
    <>
      <div>
        <Link to="/">Home</Link> | 
        <Link to="/profile">Profile</Link> | 
        <Link to="/products">Product</Link>
      </div>
      <Routes>
        <Route path='/' element={ <Home /> } />
        <Route path='/profile' element={ <Profile /> }>
          <Route path='/profile/changepassword' element={<ChangePassword /> } />
        </Route>
        <Route path='/products' element={ <Product /> } />
        <Route path='*' element={<NoMatch/> } />
      </Routes>
    </>
  )
}

export default App
