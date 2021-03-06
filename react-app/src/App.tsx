import React from 'react';
import './App.css';
import { Header } from './components/AppHeader/Header';
import { PageLayout } from './components/Pages/PageLayout';

export const App = () => {
  const [page, setPage] = React.useState<number>(4);
  const [isLoggedIn, setIsLoggedIn] = React.useState<boolean>(false);
  
  const changePage = (newPage: number) => {
    setPage(newPage);
    // Think about validations...    
  }

  return (
    <div className="root">
      <Header 
        changePage={changePage}
        isLoggedIn={isLoggedIn}
        setIsLoggedIn={setIsLoggedIn}
      />
      <PageLayout 
        page={page}
        setPage={setPage}
        isLoggedIn={isLoggedIn}
        setIsLoggedIn={setIsLoggedIn}
      />
    </div>
  );
}

export default App;
