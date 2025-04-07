import { HttpErrorResponse, HttpParams, HttpStatusCode } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { RequestMapper, ResponseMapper } from '@core/base';
import { ISignInReadableRepository } from '@core/domain';
import { SignInResponse, SignInErrorResponse, SignInRequest } from '@core/models';
import { ReadableRepository } from '@infrastructure/base';
import { catchError, map, Observable, of, tap } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class SignInReadableRepository extends ReadableRepository implements ISignInReadableRepository {
  signIn(request: SignInRequest): Observable<SignInResponse | SignInErrorResponse> {
    const body = new HttpParams().set('username', request.username).set('password', request.password);
    const endPoint = `${this._context.endPoint}/login`;
    return this.httpClient.post(endPoint, body).pipe(
      map((response) => new ResponseMapper(SignInResponse).map(response)),
      tap((data) => console.log(data)),
      catchError((error: HttpErrorResponse) => {
        let errorMapper: ResponseMapper<SignInErrorResponse>;
        if (error.status === HttpStatusCode.Unauthorized) {
          errorMapper = new ResponseMapper(SignInErrorResponse);
          return of(errorMapper.map(error.error));
        } else if (error.status === HttpStatusCode.BadRequest) {
          errorMapper = new ResponseMapper(SignInErrorResponse);
          return of(errorMapper.map(error.error));
        } else if (error.status === 0) {
          errorMapper = new ResponseMapper(SignInErrorResponse);
          return of(errorMapper.map({ title: 'Connection Error', statusCode: HttpStatusCode.InternalServerError, detail: 'Unable to connect to the server' }));
        } else {
          errorMapper = new ResponseMapper(SignInErrorResponse);
          return of(errorMapper.map({ title: 'Internal Server Error', statusCode: HttpStatusCode.InternalServerError, detail: 'An error occurred while processing your request' }));
        }
      }),
    );
  }
}
