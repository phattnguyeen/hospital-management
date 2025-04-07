import { propertyMapper } from '@core/base';

export class SignInResponse {
  @propertyMapper('access_token', String)
  public access_token: string = '';

  @propertyMapper('token_type', String)
  public token_type: string = ''; 
}
