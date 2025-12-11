@auth.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    # VALIDATION: Không được để trống
    if not username or not password:
        return render_template('login.html', error="Vui lòng nhập đủ thông tin")
    
    user = User.query.filter_by(username=username).first()
    
    # VALIDATION: Kiểm tra user tồn tại và password đúng
    if not user or not user.check_password(password):
        return render_template('login.html', error="Sai thông tin đăng nhập")
    
    # VALIDATION: Kiểm tra user active
    if not user.is_active:
        return render_template('login.html', error="Tài khoản đã bị khóa")
    
    login_user(user)
    return redirect("/auth/dashboard")
