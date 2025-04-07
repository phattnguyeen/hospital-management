import { IReadableRepository } from '@core/base';
import { SignInErrorResponse, SignInRequest, SignInResponse } from '@core/models';
import { Observable } from 'rxjs';

export interface ISignInReadableRepository extends IReadableRepository {
  signIn(request: SignInRequest): Observable<SignInResponse | SignInErrorResponse>;
}
