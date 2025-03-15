import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { catchError } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private apiUrl = 'https://hospital-management-qxwo.onrender.com';

  constructor(private http: HttpClient) { }

  /** 
   * Get stored token 
   */
  private getToken(): string | null {
    return localStorage.getItem('access_token');
  }

  /**
   * Login - Sends credentials to FastAPI OAuth2
   */
  login(credentials: { username: string; password: string }): Observable<any> {
    const body = new HttpParams()
      .set('username', credentials.username)
      .set('password', credentials.password);

    return this.http.post<any>(`${this.apiUrl}/login`, body.toString(), {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    });
  }

  /**
   * Logout - Clears stored token
   */
  logout(): void {
    localStorage.removeItem('access_token');
  }

  /**
   * Check if user is logged in
   */
  isLoggedIn(): boolean {
    return !!this.getToken();
  }

  /**
   * Fetch data from an endpoint (Authenticated)
   */
  getData(endpoint: string): Observable<any> {
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${this.getToken()}`  // Attach token
    });

    return this.http.get<any>(`${this.apiUrl}/${endpoint}`, { headers })
      .pipe(
        catchError((error) => {
          console.error('API error:', error);
          throw error;
        })
      );
  }

  /**
   * Post data to an endpoint (Authenticated)
   */
  postData(endpoint: string, data: any): Observable<any> {
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${this.getToken()}`,
      'Content-Type': 'application/json'
    });

    return this.http.post<any>(`${this.apiUrl}/${endpoint}`, data, { headers })
      .pipe(
        catchError((error) => {
          console.error('API error:', error);
          throw error;
        })
      );
  }
}
