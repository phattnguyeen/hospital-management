import { Observable } from 'rxjs';

/**
 * Defines Request Handler interface to handle domain business action
 * TRequest  -> Generic type with Request
 * TResponse -> Generic type with Response
 */
export interface RequestHandler<TRequest, TResponse> {
  /**
   * To call the repository to take the data from backend.
   * DDD to handle any type of domain business.
   * @param request
   */
  handle(request: TRequest): Observable<TResponse> | undefined;
}
