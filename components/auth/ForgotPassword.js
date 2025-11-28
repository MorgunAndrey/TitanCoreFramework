import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';

function ForgotPassword({ csrfToken, setCsrfToken }) {
    const [email, setEmail] = useState('');
    const [error, setError] = useState('');
    const navigate = useNavigate();
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
            const response = await fetch('/password/email', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: new URLSearchParams({
                    email: email,
                    csrf_token: csrfToken
                })
            });

            const data = await response.json();

            if (data.result === 1) {
                alert('Инструкции по восстановлению пароля отправлены на вашу почту');
                window.location.href = '/';
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
                            <label className="auth_label" htmlFor="email">Введите ваш E-mail</label>
                            <input 
                                id="email" 
                                className="form-control" 
                                name="email" 
                                type="email"
                                pattern="[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
                                minLength="8" 
                                maxLength="30" 
                                title="Пожалуйста, введите корректный email (например: example@domain.com)"
                                required
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                disabled={isSubmitting}
                            />
                        </div>
                        <input type="hidden" className="csrf_token" name="csrf_token" value={csrfToken} />
                        <div style={{ display: 'flex', gap: '10px', marginTop: '20px' }}>
                            <button 
                                type="submit" 
                                className="btn btn-success"
                                disabled={isSubmitting}
                            >
                                {isSubmitting ? 'Восстановить пароль' : 'Восстановить пароль'}
                            </button>
                            
                            <button 
                                type="button" 
                                className="btn btn-primary"
                                onClick={() => navigate('/login')}
                                disabled={isSubmitting}
                            >
                                Назад
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    );
}

export default ForgotPassword;