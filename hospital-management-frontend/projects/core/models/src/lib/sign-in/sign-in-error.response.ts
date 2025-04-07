import { propertyMapper } from '@core/base';

export class SignInErrorResponse {

  @propertyMapper('detail', String)
  public detail: string;

  constructor( detail: string = '') {

    this.detail = detail;
  }
}
