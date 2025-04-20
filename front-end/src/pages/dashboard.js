import { useEffect } from 'react';
import '../styles/app.css';
import Header from '../components/header';
import Sidebar from '../components/sidebar';
import TimeLine from '../components/timeline';

export default function Dashboard() {
    useEffect(() => {
        document.title = 'Instagram';
    }, []);

    return (
        <div className="bg-gray-background">
            <Header/>
            <div className='grid'>
                <TimeLine />
                <Sidebar />
            </div>
        </div>
    );
}