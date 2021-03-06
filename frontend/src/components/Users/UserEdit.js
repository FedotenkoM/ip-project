import React from 'react';
import {
  Edit,
  SimpleForm,
  TextInput,
  ReferenceInput,
  AutocompleteInput,
} from 'react-admin';
import { EntityTitle, EditActions } from '../utils';

const UserEdit = (props) => (
  <Edit title={<EntityTitle filedName="displayName" />} undoable={false} actions={<EditActions />} {...props}>
    <SimpleForm>
      <TextInput disabled source="id" label="Идентификатор" />
      <TextInput disabled source="username" label="Логин" />
      <TextInput source="password" label="Пароль" />
      <ReferenceInput source="roleId" reference="roles" label="Роль">
        <AutocompleteInput optionText="displayName" />
      </ReferenceInput>
    </SimpleForm>
  </Edit>
);

export default UserEdit;
