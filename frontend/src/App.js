import React from 'react';
import { Admin, Resource } from 'react-admin';
import polyglotI18nProvider from 'ra-i18n-polyglot';
import russianMessages from 'ra-language-russian';
import dataProvider from './api/dataProvider';
import authProvider from './api/authProvider';

import './App.less';

import { checkAppAction } from './utils';
import UserList from './components/Users/UserList';
import UserShow from './components/Users/UserShow';
import UserCreate from './components/Users/UserCreate';
import UserEdit from './components/Users/UserEdit';
import RoleList from './components/Roles/RoleList';
import RoleShow from './components/Roles/RoleShow';

const i18nProvider = polyglotI18nProvider(() => russianMessages, 'ru');

const App = () => (
  <Admin title="Flower System" dataProvider={dataProvider} authProvider={authProvider} i18nProvider={i18nProvider}>
    {(permissions) => [
      permissions.users
        ? (
          <Resource
            name="users"
            list={UserList}
            show={UserShow}
            create={checkAppAction(permissions.users, 'create') ? UserCreate : null}
            edit={checkAppAction(permissions.users, 'update') ? UserEdit : null}
            options={{ label: 'Пользователи' }}
          />
        ) : null,
      permissions.users
        ? (
          <Resource
            name="roles"
            list={RoleList}
            options={{ label: 'Роли' }}
            show={RoleShow}
          />
        ) : null,
    ]}
  </Admin>
);

export default App;
