import React from 'react';
import './App.css';
import { Header } from './components/AppHeader/Header';
import { PageLayout } from './components/Pages/PageLayout';

export const App = () => {
  const [page, setPage] = React.useState<number>(0);
  const [failedLogin, setFailedLogin] = React.useState<boolean>(false);

  const changePage = (newPage: number) => {
    setPage(newPage);
    // Think about validations...    
  }

  return (
    <div className="root">
      <Header changePage={changePage}/>
      <PageLayout 
        page={page}
        failedLogin={failedLogin}
        setFailedLogin={setFailedLogin}
      />
    </div>
  );
}

export default App;
