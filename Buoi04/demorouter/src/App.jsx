// import { Routes, Route, Link} from 'react-router-dom'
import { Link, Routes, Route } from 'react-router'
import { Home } from './components/Home'
import { Product } from './components/Product'
import { Profile, ChangePassword, Users, User } from './components/Profile'
import { NoMatch } from './components/NoMatch'
function App() {
  const users = [
    { id: '1', fullName: 'Lê Li La' },
    { id: '2', fullName: 'Hoàng Lê' },
  ];
  return (
    <>
      <nav>
        <Link to="/">Home</Link> | 
        <Link to="/profile">Profile</Link> | 
        <Link to="/products">Product</Link>
      </nav>
      <Routes>
        <Route path='/' element={ <Home /> } />
        <Route path='profile' element={ <Profile /> }>
          <Route path='changepassword' element={<ChangePassword /> } />
        </Route>
        <Route path='/products' element={ <Product /> } />
        <Route path="users" element={<Users users={users} />} />
        <Route path="users/:userId" element={<User />} />
        <Route path='*' element={<NoMatch/> } />
      </Routes>
    </>
  )
}

export default App
