package com.musinsa.crawler.domain.repository;

import com.musinsa.crawler.domain.entity.SocialCrawlAccount;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface SocialCrawlAccountRepository extends JpaRepository<SocialCrawlAccount, Long> {

    List<SocialCrawlAccount> findByPlatformId(String platformId);

    List<SocialCrawlAccount> findByStatus(String status);

    boolean existsByPlatformIdAndLoginId(String platformId, String loginId);
}
