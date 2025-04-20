import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import { Suspense, lazy } from 'react';
import * as ROUTES from './constants/routes';
import useAuthListener from './hooks/use-auth-listener';
import UserContext from './context/user';
import './styles/app.css';

const Login = lazy(() => import ('./pages/login'));
const Signup = lazy(() => import ('./pages/sign-up'));
const Dashboard = lazy(() => import ('./pages/dashboard'));
const NotFound = lazy(() => import ('./pages/not-found'));

export default function App() {
  const { user } = useAuthListener();
  return (
    <UserContext.Provider value={{user}}>
      <Router>
        <Suspense fallback={<p>Loading ... </p>}>
          <Routes>
            <Route path={ROUTES.LOGIN} element={<Login />} />
            <Route path={ROUTES.SIGN_UP} element={<Signup />} />
            <Route path={ROUTES.DASHBOARD} element={<Dashboard />} />
            <Route path="*" element={<NotFound />} />
          </Routes>
        </Suspense>
      </Router>
    </UserContext.Provider>

  );
}
