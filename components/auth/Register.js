import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';

function Register({ csrfToken, setCsrfToken }) {
    const [name, setName] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [repeatPassword, setRepeatPassword] = useState('');
    const [error, setError] = useState('');
    const [passwordError, setPasswordError] = useState('');
    const navigate = useNavigate();
    const [isSubmitting, setIsSubmitting] = useState(false);
    const timeoutRef = useRef(null);

    
    useEffect(() => {
        return () => {
            if (timeoutRef.current) clearTimeout(timeoutRef.current);
        };
    }, []);

    useEffect(() => {
        if (password && repeatPassword && password !== repeatPassword) {
            setPasswordError('Пароли не совпадают');
        } else {
            setPasswordError('');
        }
    }, [password, repeatPassword]);

    const handleSubmit = async (e) => {
        e.preventDefault();
        
        if (password !== repeatPassword) {
            setError('Пароли не совпадают');
            return;
        }
        
        setIsSubmitting(true);
        
        if (timeoutRef.current) clearTimeout(timeoutRef.current);
        
        try {
            const response = await fetch('/site/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: new URLSearchParams({
                    name: name,
                    email: email,
                    password: password,
                    csrf_token: csrfToken
                })
            });

            const data = await response.json();

            if (data.result === 1) {
                alert('Вы успешно прошли регистрацию');
                window.location.href = '/login';
            } else {
                setError(data.error);
                if (data.csrf) {
                    setCsrfToken(data.csrf);  
                }
                
                timeoutRef.current = setTimeout(() => {
                    setIsSubmitting(false);
                    setError('\u00A0');
                }, 3000);
            }
        } catch (err) {
            setError('Ошибка отправки почты');
            timeoutRef.current = setTimeout(() => {
                setIsSubmitting(false);
                setError('\u00A0');
            }, 3000);
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
                            <label className="auth_label" htmlFor="name">Введите ваше Имя</label>
                            <input 
                                id="name" 
                                className="form-control" 
                                name="name" 
                                type="text"
                                minLength="2" 
                                maxLength="30" 
                                title="Имя должно содержать только английские и/или русские буквы (от 2 до 30 символов)"
                                required
                                pattern="^[a-zA-Zа-яА-ЯёЁ\s\-]{2,30}$"
                                value={name}
                                onChange={(e) => setName(e.target.value)}
                                disabled={isSubmitting}
                            />
                        </div>
                        <div className="form-group form-animation">
                            <label className="auth_label" htmlFor="email">Введите ваш E-mail</label>
                            <input 
                                id="email" 
                                className="form-control" 
                                name="email" 
                                type="email"
                                minLength="8" 
                                maxLength="30" 
                                title="Пожалуйста, введите корректный email (например: example@domain.com)"
                                required
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                disabled={isSubmitting}
                            />
                        </div>
                         <div className="form-group form-animation">
                            <label className="auth_label" htmlFor="password">Придумайте пароль не менее 8 знаков</label>
                            <input 
                                id="password" 
                                title="Пароль должен состоять из цифр, латинских маленьких и заглавных букв, не менее 8 символов"
                                className="form-control" 
                                placeholder="" 
                                name="password" 
                                pattern="^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,30}$"
                                minLength="8" 
                                maxLength="30" 
                                type="password" 
                                required
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                disabled={isSubmitting}
                            />
                        </div>
                         <div className="form-group form-animation">
                            <label className="auth_label" htmlFor="repeat_password">Повторите пароль</label>
                            <input 
                                id="repeat_password" 
                                title="Пароль должен состоять из цифр, латинских маленьких и заглавных букв, не менее 8 символов"
                                className="form-control" 
                                placeholder="" 
                                name="repeat_password" 
                                pattern="^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,30}$"
                                minLength="8" 
                                maxLength="30" 
                                type="password" 
                                required
                                value={repeatPassword}
                                onChange={(e) => setRepeatPassword(e.target.value)}
                                disabled={isSubmitting}
                            />
                            {passwordError && (
                                <div style={{color: 'red', fontSize: '12px', marginTop: '5px'}}>
                                    {passwordError}
                                </div>
                            )}
                        </div>
                        
                        <div className="form-auth-submit">
                            <input 
                                type="submit" 
                                className="btn btn-primary  form-control confirm-auth" 
                                value="Зарегистрироваться"
                                disabled={isSubmitting || passwordError}
                            />
                        </div> 
                        <input type="hidden" className="csrf_token" name="csrf_token" value={csrfToken} />
                    </form>
                </div>
            </div>
          
        </div>
    );
}

export default Register;