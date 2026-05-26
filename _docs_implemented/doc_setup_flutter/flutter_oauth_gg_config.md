**FE cần đủ 4 phần:**

1. Gọi Google login:

```dart
await supabase.auth.signInWithOAuth(
  OAuthProvider.google,
  redirectTo: 'triam://auth/callback',
);
```

2. Supabase Dashboard phải có redirect URL:

```text
triam://auth/callback
```

3. Flutter app phải cấu hình deep link để nhận `triam://auth/callback`.

Android cần khai báo intent filter trong `AndroidManifest.xml`, đại khái:

```xml
<intent-filter>
    <action android:name="android.intent.action.VIEW" />

    <category android:name="android.intent.category.DEFAULT" />
    <category android:name="android.intent.category.BROWSABLE" />

    <data
        android:scheme="triam"
        android:host="auth"
        android:path="/callback" />
</intent-filter>
```

4. Sau khi callback về app, FE kiểm tra session:

```dart
final session = supabase.auth.currentSession;
final accessToken = session?.accessToken;
```

Token này dùng gọi BE:

```http
Authorization: Bearer <access_token>
```

Vậy kết luận: **nếu FE đã cấu hình deep link rồi thì dòng code đó là đủ để bắt đầu login Google**. Nếu chưa cấu hình deep link, Google login sẽ thành công nhưng app có thể không quay lại đúng hoặc không lưu được session.
