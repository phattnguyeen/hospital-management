import { propertyMapper } from '@core/base';

export class SignInRequest {
  @propertyMapper('username', String)
  public username: string = '';

  @propertyMapper('password', String)
  public password: string = '';

  constructor(username: string = '', password: string = '') {
    this.username = username;
    this.password = password;
  } 
}
