package com.crawler.domain.entity;

import static com.querydsl.core.types.PathMetadataFactory.*;

import com.querydsl.core.types.dsl.*;

import com.querydsl.core.types.PathMetadata;
import javax.annotation.processing.Generated;
import com.querydsl.core.types.Path;


/**
 * QSocialCrawlAccount is a Querydsl query type for SocialCrawlAccount
 */
@Generated("com.querydsl.codegen.DefaultEntitySerializer")
public class QSocialCrawlAccount extends EntityPathBase<SocialCrawlAccount> {

    private static final long serialVersionUID = -361852709L;

    public static final QSocialCrawlAccount socialCrawlAccount = new QSocialCrawlAccount("socialCrawlAccount");

    public final NumberPath<Long> accountId = createNumber("accountId", Long.class);

    public final DateTimePath<java.time.LocalDateTime> createdAt = createDateTime("createdAt", java.time.LocalDateTime.class);

    public final StringPath issue = createString("issue");

    public final StringPath loginId = createString("loginId");

    public final StringPath loginPw = createString("loginPw");

    public final StringPath name = createString("name");

    public final StringPath platformId = createString("platformId");

    public final StringPath status = createString("status");

    public final DateTimePath<java.time.LocalDateTime> updatedAt = createDateTime("updatedAt", java.time.LocalDateTime.class);

    public QSocialCrawlAccount(String variable) {
        super(SocialCrawlAccount.class, forVariable(variable));
    }

    public QSocialCrawlAccount(Path<? extends SocialCrawlAccount> path) {
        super(path.getType(), path.getMetadata());
    }

    public QSocialCrawlAccount(PathMetadata metadata) {
        super(SocialCrawlAccount.class, metadata);
    }

}

