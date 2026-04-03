package com.crawler.domain.entity;

import static com.querydsl.core.types.PathMetadataFactory.*;

import com.querydsl.core.types.dsl.*;

import com.querydsl.core.types.PathMetadata;
import javax.annotation.processing.Generated;
import com.querydsl.core.types.Path;


/**
 * QSocialPlatform is a Querydsl query type for SocialPlatform
 */
@Generated("com.querydsl.codegen.DefaultEntitySerializer")
public class QSocialPlatform extends EntityPathBase<SocialPlatform> {

    private static final long serialVersionUID = -1082878008L;

    public static final QSocialPlatform socialPlatform = new QSocialPlatform("socialPlatform");

    public final DateTimePath<java.time.LocalDateTime> createdAt = createDateTime("createdAt", java.time.LocalDateTime.class);

    public final StringPath platformId = createString("platformId");

    public final StringPath platformName = createString("platformName");

    public QSocialPlatform(String variable) {
        super(SocialPlatform.class, forVariable(variable));
    }

    public QSocialPlatform(Path<? extends SocialPlatform> path) {
        super(path.getType(), path.getMetadata());
    }

    public QSocialPlatform(PathMetadata metadata) {
        super(SocialPlatform.class, metadata);
    }

}

