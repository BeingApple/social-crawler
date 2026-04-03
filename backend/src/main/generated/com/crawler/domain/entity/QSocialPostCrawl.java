package com.crawler.domain.entity;

import static com.querydsl.core.types.PathMetadataFactory.*;

import com.querydsl.core.types.dsl.*;

import com.querydsl.core.types.PathMetadata;
import javax.annotation.processing.Generated;
import com.querydsl.core.types.Path;


/**
 * QSocialPostCrawl is a Querydsl query type for SocialPostCrawl
 */
@Generated("com.querydsl.codegen.DefaultEntitySerializer")
public class QSocialPostCrawl extends EntityPathBase<SocialPostCrawl> {

    private static final long serialVersionUID = 486931122L;

    public static final QSocialPostCrawl socialPostCrawl = new QSocialPostCrawl("socialPostCrawl");

    public final StringPath accountId = createString("accountId");

    public final StringPath accountType = createString("accountType");

    public final NumberPath<Long> authorFollowers = createNumber("authorFollowers", Long.class);

    public final StringPath authorName = createString("authorName");

    public final StringPath brandName = createString("brandName");

    public final NumberPath<Long> commentCount = createNumber("commentCount", Long.class);

    public final StringPath crawlCase = createString("crawlCase");

    public final DateTimePath<java.time.LocalDateTime> createdAt = createDateTime("createdAt", java.time.LocalDateTime.class);

    public final BooleanPath duplicate = createBoolean("duplicate");

    public final StringPath hashtags = createString("hashtags");

    public final BooleanPath junk = createBoolean("junk");

    public final NumberPath<Long> likeCount = createNumber("likeCount", Long.class);

    public final StringPath matchedKeywords = createString("matchedKeywords");

    public final StringPath mediaUrl = createString("mediaUrl");

    public final StringPath personTags = createString("personTags");

    public final StringPath platformId = createString("platformId");

    public final DateTimePath<java.time.LocalDateTime> postedAt = createDateTime("postedAt", java.time.LocalDateTime.class);

    public final StringPath postId = createString("postId");

    public final StringPath postTitle = createString("postTitle");

    public final StringPath postType = createString("postType");

    public final StringPath postUrl = createString("postUrl");

    public final MapPath<String, Object, SimplePath<Object>> rawData = this.<String, Object, SimplePath<Object>>createMap("rawData", String.class, Object.class, SimplePath.class);

    public final NumberPath<Long> shareCount = createNumber("shareCount", Long.class);

    public final NumberPath<Long> spcId = createNumber("spcId", Long.class);

    public final StringPath textContent = createString("textContent");

    public final StringPath thumbnailUrl = createString("thumbnailUrl");

    public final DateTimePath<java.time.LocalDateTime> updatedAt = createDateTime("updatedAt", java.time.LocalDateTime.class);

    public final NumberPath<Long> viewCount = createNumber("viewCount", Long.class);

    public QSocialPostCrawl(String variable) {
        super(SocialPostCrawl.class, forVariable(variable));
    }

    public QSocialPostCrawl(Path<? extends SocialPostCrawl> path) {
        super(path.getType(), path.getMetadata());
    }

    public QSocialPostCrawl(PathMetadata metadata) {
        super(SocialPostCrawl.class, metadata);
    }

}

