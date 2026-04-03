package com.crawler.domain.entity;

import static com.querydsl.core.types.PathMetadataFactory.*;

import com.querydsl.core.types.dsl.*;

import com.querydsl.core.types.PathMetadata;
import javax.annotation.processing.Generated;
import com.querydsl.core.types.Path;


/**
 * QSocialCrawlExcludeKeyword is a Querydsl query type for SocialCrawlExcludeKeyword
 */
@Generated("com.querydsl.codegen.DefaultEntitySerializer")
public class QSocialCrawlExcludeKeyword extends EntityPathBase<SocialCrawlExcludeKeyword> {

    private static final long serialVersionUID = 1342777409L;

    public static final QSocialCrawlExcludeKeyword socialCrawlExcludeKeyword = new QSocialCrawlExcludeKeyword("socialCrawlExcludeKeyword");

    public final BooleanPath active = createBoolean("active");

    public final NumberPath<Long> brandId = createNumber("brandId", Long.class);

    public final DateTimePath<java.time.LocalDateTime> createdAt = createDateTime("createdAt", java.time.LocalDateTime.class);

    public final StringPath createdBy = createString("createdBy");

    public final StringPath description = createString("description");

    public final StringPath filterKeyword = createString("filterKeyword");

    public final StringPath junkKeyword = createString("junkKeyword");

    public final NumberPath<Long> keywordId = createNumber("keywordId", Long.class);

    public final StringPath keywordType = createString("keywordType");

    public final StringPath matchType = createString("matchType");

    public final StringPath platformId = createString("platformId");

    public final DateTimePath<java.time.LocalDateTime> updatedAt = createDateTime("updatedAt", java.time.LocalDateTime.class);

    public QSocialCrawlExcludeKeyword(String variable) {
        super(SocialCrawlExcludeKeyword.class, forVariable(variable));
    }

    public QSocialCrawlExcludeKeyword(Path<? extends SocialCrawlExcludeKeyword> path) {
        super(path.getType(), path.getMetadata());
    }

    public QSocialCrawlExcludeKeyword(PathMetadata metadata) {
        super(SocialCrawlExcludeKeyword.class, metadata);
    }

}

