package com.musinsa.crawler.service;

import com.musinsa.crawler.api.dto.SocialCrawlAccountCredentialResponse;
import com.musinsa.crawler.api.dto.SocialCrawlAccountRequest;
import com.musinsa.crawler.api.dto.SocialCrawlAccountResponse;
import com.musinsa.crawler.common.AesEncryptionUtil;
import com.musinsa.crawler.domain.entity.SocialCrawlAccount;
import com.musinsa.crawler.domain.repository.SocialCrawlAccountRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.NoSuchElementException;

@Service
@RequiredArgsConstructor
@Transactional(readOnly = true)
public class SocialCrawlAccountService {

    private final SocialCrawlAccountRepository repository;
    private final AesEncryptionUtil encryption;

    /** 전체 목록 — loginId 복호화하여 반환, loginPw 미포함 */
    public List<SocialCrawlAccountResponse> findAll() {
        return repository.findAll().stream()
                .map(e -> SocialCrawlAccountResponse.from(e, encryption.decrypt(e.getLoginId())))
                .toList();
    }

    /** 단건 조회 — loginId 복호화하여 반환, loginPw 미포함 */
    public SocialCrawlAccountResponse findById(Long accountId) {
        SocialCrawlAccount entity = getOrThrow(accountId);
        return SocialCrawlAccountResponse.from(entity, encryption.decrypt(entity.getLoginId()));
    }

    /** loginId + loginPw 원문 복호화하여 반환 */
    public SocialCrawlAccountCredentialResponse decrypt(Long accountId) {
        SocialCrawlAccount entity = getOrThrow(accountId);
        return SocialCrawlAccountCredentialResponse.builder()
                .accountId(entity.getAccountId())
                .platformId(entity.getPlatformId())
                .loginId(encryption.decrypt(entity.getLoginId()))
                .loginPw(encryption.decrypt(entity.getLoginPw()))
                .build();
    }

    /** 생성 — loginId, loginPw 암호화하여 저장 */
    @Transactional
    public SocialCrawlAccountResponse create(SocialCrawlAccountRequest req) {
        SocialCrawlAccount entity = SocialCrawlAccount.builder()
                .name(req.getName())
                .platformId(req.getPlatformId())
                .loginId(encryption.encrypt(req.getLoginId()))
                .loginPw(encryption.encrypt(req.getLoginPw()))
                .issue(req.getIssue())
                .status(req.getStatus())
                .build();

        SocialCrawlAccount saved = repository.save(entity);
        return SocialCrawlAccountResponse.from(saved, req.getLoginId());
    }

    /** 수정 — loginId, loginPw 재암호화하여 저장 */
    @Transactional
    public SocialCrawlAccountResponse update(Long accountId, SocialCrawlAccountRequest req) {
        SocialCrawlAccount entity = getOrThrow(accountId);
        entity.update(
                req.getName(),
                req.getPlatformId(),
                encryption.encrypt(req.getLoginId()),
                encryption.encrypt(req.getLoginPw()),
                req.getIssue(),
                req.getStatus()
        );
        return SocialCrawlAccountResponse.from(entity, req.getLoginId());
    }

    /** 삭제 */
    @Transactional
    public void delete(Long accountId) {
        if (!repository.existsById(accountId)) {
            throw new NoSuchElementException("account not found: " + accountId);
        }
        repository.deleteById(accountId);
    }

    private SocialCrawlAccount getOrThrow(Long accountId) {
        return repository.findById(accountId)
                .orElseThrow(() -> new NoSuchElementException("account not found: " + accountId));
    }
}
