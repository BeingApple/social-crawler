package com.musinsa.crawler.domain.repository;

import com.musinsa.crawler.domain.entity.QSocialPostCrawl;
import com.musinsa.crawler.domain.entity.SocialPostCrawl;
import com.querydsl.core.BooleanBuilder;
import com.querydsl.jpa.impl.JPAQueryFactory;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageImpl;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Repository;

import java.time.LocalDateTime;
import java.util.List;

@Repository
@RequiredArgsConstructor
public class SocialPostCrawlRepositoryImpl implements SocialPostCrawlRepositoryCustom {

    private final JPAQueryFactory queryFactory;

    @Override
    public Page<SocialPostCrawl> findWithFilters(
            String platformId,
            String brandName,
            String crawlCase,
            String accountType,
            LocalDateTime postedFrom,
            LocalDateTime postedTo,
            Pageable pageable
    ) {
        QSocialPostCrawl post = QSocialPostCrawl.socialPostCrawl;
        BooleanBuilder where = new BooleanBuilder();

        if (platformId  != null && !platformId.isBlank())  where.and(post.platformId.eq(platformId));
        if (brandName   != null && !brandName.isBlank())   where.and(post.brandName.containsIgnoreCase(brandName));
        if (crawlCase   != null && !crawlCase.isBlank())   where.and(post.crawlCase.eq(crawlCase));
        if (accountType != null && !accountType.isBlank()) where.and(post.accountType.eq(accountType));
        if (postedFrom  != null)                           where.and(post.postedAt.goe(postedFrom));
        if (postedTo    != null)                           where.and(post.postedAt.lt(postedTo));

        List<SocialPostCrawl> content = queryFactory
                .selectFrom(post)
                .where(where)
                .orderBy(post.createdAt.desc())
                .offset(pageable.getOffset())
                .limit(pageable.getPageSize())
                .fetch();

        long total = queryFactory
                .select(post.count())
                .from(post)
                .where(where)
                .fetchOne();

        return new PageImpl<>(content, pageable, total);
    }
}
