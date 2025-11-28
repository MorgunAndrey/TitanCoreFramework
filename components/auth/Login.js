// components/auth/Login.js
import React, { useState, useEffect, useRef } from 'react';

function Login({ csrfToken, setCsrfToken }) {  // Добавляем setCsrfToken в пропсы
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [isSubmitting, setIsSubmitting] = useState(false);

    const timeoutRef = useRef(null);

    useEffect(() => {
        return () => {
            if (timeoutRef.current) clearTimeout(timeoutRef.current);
        };
    }, []);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setIsSubmitting(true);
        
        if (timeoutRef.current) clearTimeout(timeoutRef.current);
        
        try {
            const response = await fetch('/auth/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: new URLSearchParams({
                    login: email,
                    password: password,
                    csrf_token: csrfToken
                })
            });
            
            const data = await response.json();
            
            if (data.result === 1) {
                window.location.href = data.url;
            } else {
                setError(data.error);
                if (data.csrf) {
                    setCsrfToken(data.csrf);  // Обновляем CSRF-токен, если он пришел
                }
                
                timeoutRef.current = setTimeout(() => {
                    setIsSubmitting(false);
                    setError('\u00A0');
                }, 3000);
                
                return;
            }
        } catch (err) {
            setError('Ошибка сети или сервера');
            timeoutRef.current = setTimeout(() => {
                setIsSubmitting(false);
                setError('\u00A0');
            }, 3000);
        } finally {
            setIsSubmitting(false);
        }
    };

    return (
        <div id="page-auth">
              <div className="page-wrapper">             
                <div id="form_auth" className="form-auth">
                    <div className="jsError" style={{margin: '0px 20px 10px 10px', color: 'red', fontSize: '12px', textAlign: 'center'}}>
                        {error || '\u00A0'}
                    </div>
                    
                    <form onSubmit={handleSubmit}>
                        <div className="form-group form-animation">
                            <label className="auth_label" htmlFor="i_name">E-mail</label>
                            <input 
                                id="i_name" 
                                className="form-control"
                                name="login" 
                                type="email"
                                pattern="[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
                                minLength="8" 
                                maxLength="30" 
                                title="Пожалуйста, введите корректный email (например: example@domain.com)"
                                required
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                            />
                        </div>
                        <div className="form-group form-animation">
                            <label className="auth_label" htmlFor="i_password">Пароль</label>
                            <input 
                                id="i_password" 
                                title="Пароль должен состоять из цифр, латинских маленьких и заглавных букв, не менее 8 символов"
                                className="form-control"  
                                name="password" 
                                pattern="((?=^.{7,}$)(?=.*[A-Z])(?=.*[0-9])(?=.*[a-z])[a-zA-Z0-9]*)" 
                                minLength="8" 
                                maxLength="30" 
                                type="password" 
                                required
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                            />
                        </div>
                        <input type="hidden" className="csrf_token" name="csrf_token" value={csrfToken} />
                        <div className="form-auth-submit">
                            <input 
                                type="submit" 
                                className="btn btn-primary  form-control confirm-auth" 
                                value="Войти"
                                disabled={isSubmitting}
                            />
                        </div> 
                    </form>
                    <br></br>
                    <a href="/forgot/password" className="btn_reset_password">Забыли пароль?</a>
                </div>
            </div>
        </div>    
    );
}

export default Login;




