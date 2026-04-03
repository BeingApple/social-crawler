package com.crawler.common;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

import javax.crypto.Cipher;
import javax.crypto.spec.GCMParameterSpec;
import javax.crypto.spec.SecretKeySpec;
import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.security.SecureRandom;
import java.util.Arrays;
import java.util.Base64;

/**
 * AES-256-GCM 암복호화 유틸
 *
 * <p>저장 형식: Base64( IV[12 bytes] || GCM_Ciphertext+AuthTag )
 * <p>키 도출: 환경변수 ENCRYPTION_SECRET_KEY 문자열을 SHA-256 해싱 → 256-bit AES 키
 */
@Component
public class AesEncryptionUtil {

    private static final String ALGORITHM     = "AES/GCM/NoPadding";
    private static final int    GCM_TAG_BITS  = 128;
    private static final int    IV_LENGTH     = 12;

    private final SecretKeySpec secretKey;
    private final SecureRandom  secureRandom  = new SecureRandom();

    public AesEncryptionUtil(@Value("${encryption.secret-key}") String rawKey) {
        try {
            MessageDigest sha = MessageDigest.getInstance("SHA-256");
            byte[] keyBytes = sha.digest(rawKey.getBytes(StandardCharsets.UTF_8));
            this.secretKey = new SecretKeySpec(keyBytes, "AES");
        } catch (Exception e) {
            throw new IllegalStateException("AES 키 초기화 실패", e);
        }
    }

    /** 평문 → Base64 인코딩된 암호문 (IV 포함) */
    public String encrypt(String plaintext) {
        try {
            byte[] iv = new byte[IV_LENGTH];
            secureRandom.nextBytes(iv);

            Cipher cipher = Cipher.getInstance(ALGORITHM);
            cipher.init(Cipher.ENCRYPT_MODE, secretKey, new GCMParameterSpec(GCM_TAG_BITS, iv));
            byte[] ciphertext = cipher.doFinal(plaintext.getBytes(StandardCharsets.UTF_8));

            byte[] combined = new byte[IV_LENGTH + ciphertext.length];
            System.arraycopy(iv, 0, combined, 0, IV_LENGTH);
            System.arraycopy(ciphertext, 0, combined, IV_LENGTH, ciphertext.length);

            return Base64.getEncoder().encodeToString(combined);
        } catch (Exception e) {
            throw new IllegalStateException("암호화 실패", e);
        }
    }

    /** Base64 인코딩된 암호문 → 평문 */
    public String decrypt(String encrypted) {
        try {
            byte[] combined    = Base64.getDecoder().decode(encrypted);
            byte[] iv          = Arrays.copyOfRange(combined, 0, IV_LENGTH);
            byte[] ciphertext  = Arrays.copyOfRange(combined, IV_LENGTH, combined.length);

            Cipher cipher = Cipher.getInstance(ALGORITHM);
            cipher.init(Cipher.DECRYPT_MODE, secretKey, new GCMParameterSpec(GCM_TAG_BITS, iv));
            return new String(cipher.doFinal(ciphertext), StandardCharsets.UTF_8);
        } catch (Exception e) {
            throw new IllegalStateException("복호화 실패", e);
        }
    }
}
