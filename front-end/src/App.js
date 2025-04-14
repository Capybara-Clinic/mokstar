import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import { Suspense, lazy } from 'react';

const Login = lazy(() => import ('./pages/login'));

function App() {
  return (
    <Router>
      <Suspense fallback={<p>Loading ... </p>}>
        <Routes>
          <Route path="/login" element={<Login />} />
        </Routes>
      </Suspense>
    </Router>
  );
}

export default App;
