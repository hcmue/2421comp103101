import {useParams, Link} from 'react-router'

export const Profile =() => {
    return (
        <div>
            <h2>MY PROFILE</h2>
            <div>My name :</div>
        </div>
    )
}

export const ChangePassword =() => {
    return (
        <div>
            <h2>CHANGE PASSWORD</h2>
            <div>Old password :</div>
            <div>New password :</div>
            <div>Confirm New password :</div>
        </div>
    )
}

export const Users = ({ users }) => {
  return (
    <>
      <h2>Users</h2>
      <ul>
        {users.map((user) => (
          <li key={user.id}>
            <Link to={user.id}>{user.fullName}</Link>
          </li>
        ))}
      </ul>
    </>
  );
};

export const User = () => {
  const { userId } = useParams();
  return (
    <>
      <h2>User: {userId}</h2>
      <Link to="/users">Back to Users</Link>
    </>
  );
};